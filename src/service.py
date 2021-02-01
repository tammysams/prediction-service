from src.housekeeping import CleansListAPI

class CleanPredictionService():

    def __init__(self):
        self.cleans = CleansListAPI()

    def get_min_max_sum(self, clean_ids):
        '''
        Compute min max and sum predicted clean times from 
        data returned by Housekeeping

        :param      clean_ids: list of clean UUIDs
        :return     min, max, sum predicted clean times

        '''
        predicted_clean_times = self.cleans.list_predictions(clean_ids)
        return {
            'sum': sum(predicted_clean_times),
            'max': max(predicted_clean_times),
            'min': min(predicted_clean_times)
        }
