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
        predictions = self.cleans.list_predictions(clean_ids)
        if not predictions:
            return {
                'sum': 0,
                'min': None,
                'max': None
            }
        else:
            return {
                'sum': sum(predictions),
                'max': max(predictions),
                'min': min(predictions)
            }
