from speaker_verification import sample_from_mfcc, read_mfcc, run_user_evaluation, SAMPLE_RATE, NUM_FRAMES
class Model:

    @staticmethod
    def compare_voice(mfcc, test_voice_path):
        score = run_user_evaluation(mfcc, test_voice_path)
        score = round(score[0]*100, 2)
        return score
    
    @staticmethod
    def train_voice(path):
        mfcc = sample_from_mfcc(read_mfcc(path, SAMPLE_RATE), NUM_FRAMES)
        return mfcc