# 텍스트 분류에 필요한 것들을 담아 넘겨줄 때 사용

class Config:
    
    def __init__(self, model_fn, gpu_id, batch_size, lines):
        self.model_fn = model_fn # model full name. 모델 저장 경로
        self.gpu_id = gpu_id # cuda 사용 시, gpu id
        self.batch_size = batch_size # 모델 batch size
        self.lines = lines # 분류하고자 하는 블로그 text들
        self.top_k = 1 # probability 상위 몇 개를 출력할 것인지