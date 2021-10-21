import subprocess
import json
import traceback


def getmediasize_online(url):
    """通过ffprobe在线获取音视频时长

    Args:
        url string: 请求的音视频连接

    Returns:
        int: 时长信息
    """
    try:
        ffprobe_command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', '-i',
                           url]
        ffprobe_process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE)
        try:
            ffprobe_output = json.loads(ffprobe_process.communicate()[0].decode('utf-8', 'replace'))
        except KeyboardInterrupt:
            ffprobe_process.terminate()
            return None
        duration = 0
        for stream in dict.get(ffprobe_output, 'streams') or []:
            if float(dict.get(stream, 'duration')) > duration:
                duration = float(dict.get(stream, 'duration'))
        if duration == 0:
            return None
        return int(float(duration))
    except Exception as e:
        # logorraise(e)
        traceback.print_exc()
        return None


if __name__ == "__main__":
    url = "https://v.cece.com/hvideo_cvideo_d41ecb40165211ec820339e922e01f84.MOV"
    url = "https://v.cece.com/hvideo_cvideo_d489ed301f2611ecb36419362b2a7b86.mp4"
    url = "https://v.cece.com/hvideo_cvideo_448d23700d5e11ec9f61d3b6dd3bb84a.MP4"
    # url = "http://downsc.chinaz.net/Files/DownLoad/sound1/201906/11582.mp3"
    # url = "http://downsc.chinaz.net/files/download/sound1/201206/1638.mp3"
    url = "https://cos.ap-guangzhou.myqcloud.com/tianyu-content-moderation-1255466713/segment-/audio/w-live_video-YWZ2CKUw9Z0jaePS/1634114456.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIDdwNB137eYGCIfi1cA0RQWeuSrewMp0dZoDth7t2OYshAUWmO7lErPotB0Zzd9SpR%2F20211013%2Fap-guangzhou%2Fs3%2Faws4_request&X-Amz-Date=20211013T084111Z&X-Amz-Expires=604800&X-Amz-Security-Token=79Yit4g5xWVCmHMsX7EyHsLBPiSDnnXa58e0cc17eb00eb5a90eca7b9a5156b08-yJCTJ8cWcTizhW_SQPLtYkOLLT17jXVrWi_M8IoSx_NUXF3YbiVJDxTpb5BdXESxS3jZVGJRARRZ5aVmzp2MPzP_kZyjsPW6IvB9q9BgRvnt0MmlwfKVmLRgSACyqK1VqHSNw4rXyK-WtarLgb6xy43Zlf5MCs3dnSRnxtJjTXZf6ymdGbUI-g72KRiC_GP3wCCuEWZ6KX9BEjeSy7_IFl7iyNoyudn_KYqaf1QELCio5JVRY3ystpA4uuUHe8U7f-VHNhmmFMYBixv8GxpT0Af23wcTrgM80Tsm0-NO6QwdQlm5FhMV_8hWDD8h2PmfBZE_fAYIM3UdotBg0txyK9WunFmkkbJgR1yBMWX1zE&X-Amz-SignedHeaders=host&X-Amz-Signature=51759c56d2353bf666de3d803cb3c9b85651787384c2de951a8c14fb80d7420b"
    duration = getmediasize_online(url)
    print(duration, type(duration))
