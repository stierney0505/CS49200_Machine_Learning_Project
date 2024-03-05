import os
import pandas as pd
from typing_extensions import Self, List
from sklearn.preprocessing import MinMaxScaler

# pylint: disable=locally-disabled, line-too-long, broad-exception-caught, too-many-arguments

class Preprocessor:
    """Handles the preprocessing of ML data"""

    def __init__(self: Self, stock_file_list: List[str], currency_file_list: List[str]) -> None:
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
            new_columns.append(col + '_' + suffix)

        dataframe.columns = new_columns #PBR?

    # end rename_columns

    def concatenate(self: Self) -> pd.DataFrame:
        """Takes the stock/currency files specifed
        in the constructor and opens then concatenates
        them into a single dataframe"""
        stock_frames = []
        currency_frames = []

        # Convert CSV files into pandas dataframes
        for cur_file, stock_file in zip(self.stock_files, self.currency_files):
            stock_frames.append(pd.read_csv(stock_file))
            currency_frames.append(pd.read_csv(cur_file))

        # Rename columns
        for stock_f, currency_f, stock_df, currency_df in zip(self.stock_files, self.currency_files, stock_frames, currency_frames):
            self.rename_columns(stock_f, stock_df)
            self.rename_columns(currency_f, currency_df)

        # Concatenate all dataframes into one dataframe
        for currency_df, stock_df in zip(currency_frames, stock_frames):
            # Convert 'timestamp' column to pandas date object
            currency_df['timestamp'] = pd.to_datetime(currency_df['timestamp']).dt.date
            stock_df['timestamp'] = pd.to_datetime(stock_df['timestamp']).dt.date

            # Catch first pass where self.df is empty
            if self.df.empty:
                self.df = pd.merge(currency_df, stock_df, on='timestamp')
            else:
                self.df = self.df.merge(right=currency_df, on='timestamp')
                self.df = self.df.merge(right=stock_df, on='timestamp')

        return self.df

        # end concatenate

    def apply_preprocessing(self: Self, minmax=True, moving_average=True, moving_average_window=10, rsi_index=True) -> pd.DataFrame:
        """Applies various preprocessing options to the 
        final dataframe."""
        # Convert timestamp to numerical value
        self.df['timestamp'] = pd.to_numeric(self.df['timestamp'])

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

        return self.df

        # end apply_preprocessing

    def write_csv(self: Self, filename='output.csv'):
        '''Writes self.df to a specified output file'''
        try:
            self.df.to_csv(os.path.join(os.getcwd() + filename), index=False)
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
