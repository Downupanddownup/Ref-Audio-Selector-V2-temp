import sys
import os
import signal
import subprocess
import uvicorn

print("Current working directory:", os.getcwd())
# 将项目根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from server.api.inference_params_manager import InferenceParamsManager, InferenceParams

# 获取当前脚本所在的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 计算上上级目录的绝对路径
api_dir = os.path.join(current_dir, "../../../GPT-SoVITS-v2-240807")

# 将上上级目录添加到模块搜索路径中
sys.path.append(api_dir)

sys.path.append("%s/GPT_SoVITS" % api_dir)

# 传递命令行参数
sys.argv.extend(["--hubert_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-hubert-base")])
sys.argv.extend(["--bert_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large")])
sys.argv.extend(["--sovits_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/s2G488k.pth")])
sys.argv.extend(["--gpt_path",
                 os.path.join(api_dir, "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt")])

# 设置环境变量
os.environ['g2pw_model_dir'] = os.path.join(api_dir, "GPT_SoVITS/text/G2PWModel")
os.environ['g2pw_model_source'] = os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large")

inference_params_manager = InferenceParamsManager()

# 导入模块中的所有内容
from api import *


@app.get("/status")
async def status():
    # 发送 SIGINT 信号给当前进程
    return {"message": "server is running"}


@app.post("/ras/set_default_params")
async def set_default_params(request: Request):
    json_post_raw = await request.json()
    inference_params_manager.set_default_params(InferenceParams(
        refer_wav_path=json_post_raw.get("refer_wav_path"),
        prompt_text=json_post_raw.get("prompt_text"),
        prompt_language=json_post_raw.get("prompt_language"),
        cut_punc=json_post_raw.get("cut_punc"),
        top_k=json_post_raw.get("top_k", None),
        top_p=json_post_raw.get("top_p", None),
        temperature=json_post_raw.get("temperature", None),
        speed=json_post_raw.get("speed", None)
    ))
    return {"code": 0, "msg": "设置成功"}


@app.post("/ras")
async def tts_endpoint(request: Request):
    json_post_raw = await request.json()
    params = inference_params_manager.get_real_params(InferenceParams(
        refer_wav_path=json_post_raw.get("refer_wav_path"),
        prompt_text=json_post_raw.get("prompt_text"),
        prompt_language=json_post_raw.get("prompt_language"),
        cut_punc=json_post_raw.get("cut_punc"),
        top_k=json_post_raw.get("top_k", None),
        top_p=json_post_raw.get("top_p", None),
        temperature=json_post_raw.get("temperature", None),
        speed=json_post_raw.get("speed", None)
    ))
    return handle(
        refer_wav_path=params.refer_wav_path,
        prompt_text=params.prompt_text,
        prompt_language=params.prompt_language,
        text=json_post_raw.get("text"),
        text_language=json_post_raw.get("text_language"),
        cut_punc=params.cut_punc,
        top_k=params.top_k,
        top_p=params.top_p,
        temperature=params.temperature,
        speed=params.speed
    )


@app.get("/ras")
async def tts_endpoint(
        refer_wav_path: str = None,
        prompt_text: str = None,
        prompt_language: str = None,
        text: str = None,
        text_language: str = None,
        cut_punc: str = None,
        top_k: int = None,
        top_p: float = None,
        temperature: float = None,
        speed: float = None
):
    params = inference_params_manager.get_real_params(InferenceParams(
        refer_wav_path=refer_wav_path,
        prompt_text=prompt_text,
        prompt_language=prompt_language,
        cut_punc=cut_punc,
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        speed=speed
    ))
    return handle(
        refer_wav_path=params.refer_wav_path,
        prompt_text=params.prompt_text,
        prompt_language=params.prompt_language,
        text=text,
        text_language=text_language,
        cut_punc=params.cut_punc,
        top_k=params.top_k,
        top_p=params.top_p,
        temperature=params.temperature,
        speed=params.speed
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, workers=1)
