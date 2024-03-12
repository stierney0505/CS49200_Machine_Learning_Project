import os
import pandas as pd
from typing_extensions import Self, List
from sklearn.preprocessing import MinMaxScaler
import joblib

# pylint: disable=locally-disabled, line-too-long, broad-exception-caught, too-many-arguments

class Preprocessor:
    """Handles the preprocessing of ML data"""

    def __init__(self: Self, stock_file_list: List[str], currency_file_list: List[str]) -> None:
        self.cwd = os.getcwd() + '\\'
        self.stock_files = stock_file_list
        self.currency_files = currency_file_list
        self.df = pd.DataFrame()

    # end __init__

    def rename_columns(self: Self, file_name: str, dataframe: pd.DataFrame):
        """Applies a suffix to each column of a dataframe from it's
        filename."""
        suffix = file_name.partition('.')[0]
        columns = dataframe.columns
        new_columns = []

        for col in columns:
            if col != 'timestamp':
                new_columns.append(col + '_' + suffix)
            else:
                new_columns.append('timestamp')

        dataframe.columns = new_columns #PBR?

    # end rename_columns

    def concatenate(self: Self) -> pd.DataFrame:
        """Takes the stock/currency files specifed
        in the constructor and opens then concatenates
        them into a single dataframe"""
        stock_frames = []
        currency_frames = []

        # Convert CSV files into pandas dataframes
        for cur_file in self.currency_files:
            currency_frames.append(pd.read_csv(os.path.join(self.cwd + cur_file)))

        for stock_file in self.stock_files:
            stock_frames.append(pd.read_csv(os.path.join(self.cwd + stock_file)))


        # Rename columns
        for stock_f, stock_df in zip(self.stock_files, stock_frames):
            # Drop non-numerical column
            stock_df.drop(columns=['symbol'], axis='columns', inplace=True)
            self.rename_columns(stock_f, stock_df)

        for currency_f, currency_df in zip(self.currency_files, currency_frames):
            self.rename_columns(currency_f, currency_df)


        # Concatenate all dataframes into one dataframe
        all_frames = stock_frames + currency_frames

        for frame in all_frames:
            frame['timestamp'] = pd.to_datetime(frame['timestamp']).dt.date

            # Catch first pass where df is empty
            if self.df.empty:
                self.df = frame
            else:
                self.df = self.df.merge(right=frame, on='timestamp')

        return self.df

        # end concatenate

    def apply_preprocessing(self: Self, minmax=True, moving_average=True, moving_average_window=10, rsi_index=True) -> pd.DataFrame:
        """Applies various preprocessing options to the 
        final dataframe."""
        # Convert timestamp to numerical value
        self.df['timestamp'] = pd.to_numeric(pd.to_datetime(self.df['timestamp']))

        if moving_average:
            for col in self.df.columns:
                if col != 'timestamp':
                    self.df[col] = self.df[col].rolling(moving_average_window).mean()

        if rsi_index:
            pass #TODO

        # Apply MinMaxing from sklean (Do this last)
        if minmax:
            scaler = MinMaxScaler()
            self.df[self.df.columns] = scaler.fit_transform(self.df)

        # Drop null
        self.df.dropna(inplace=True)
        print(self.df.head())

        return self.df

        # end apply_preprocessing

    def write_csv(self: Self, filename='output.csv'):
        '''Writes self.df to a specified output file'''
        try:
            self.df.to_csv(os.path.join(self.cwd + filename), index=False)
            print("DataFrame successfully written to CSV")
        except Exception as e:
            print("Error writing DataFrame to CSV:", str(e))

    # end write_csv

    def process(self: Self, minmax=True, moving_average=True, moving_average_window=10, rsi_index=True, out_file='output.csv'):
        '''Driver method. Concatenates all data, applies
        preprocessing techniques, and writes to CSV.'''
        self.concatenate()
        self.apply_preprocessing(minmax, moving_average, moving_average_window, rsi_index)
        self.write_csv(out_file)

    # end process
    
    def save_scalers(self: Self):
        """Save scaler objects to files"""
        os.makedirs(self.scaler_directory, exist_ok=True)

        for col, scaler in self.scalers.items():
            scaler_filename = os.path.join(self.scaler_directory, col + '_scaler.joblib')
            joblib.dump(scaler, scaler_filename)
    
    def load_scalers(self: Self):
        """Load scaler objects from files"""
        for col in self.df.columns:
            if col != 'timestamp':
                scaler_filename = os.path.join(self.scaler_directory, col + '_scaler.joblib')
                self.scalers[col] = joblib.load(scaler_filename)
