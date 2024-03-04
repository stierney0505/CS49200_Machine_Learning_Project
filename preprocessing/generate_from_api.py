import pandas as pd
from typing_extensions import Self, List

# pylint: disable=locally-disabled, line-too-long

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

        dataframe.columns = new_columns

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
            currency_df['timestamp'] = pd.to_datetime(currency_df['timestamp'])
            stock_df['timestamp'] = pd.to_datetime(stock_df['timestamp'])

            # Catch first pass where self.df is empty
            if self.df.empty:
                self.df = pd.merge(currency_df, stock_df, on='timestamp')
            else:
                self.df = self.df.merge(right=currency_df, on='timestamp')
                self.df = self.df.merge(right=stock_df, on='timestamp')

        return self.df

        # end concatenate

    def apply_preprocessing(self: Self, minmax=True, moving_average=True, rsi_index=True):
        """Applies various preprocessing options to the 
        final dataframe."""
        pass

        # end apply_preprocessing