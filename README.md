# 蔚县剪纸 · 刻刀下的色彩传奇

> 一部介绍**河北蔚县剪纸**历史的短视频，全长约 3 分钟，中文配音、字幕式分镜，纯本地工具链生成。

## 视频

| 项目 | 内容 |
| --- | --- |
| 文件 | [`video/weixian-paper-cutting.mp4`](video/weixian-paper-cutting.mp4) |
| 时长 | 2 分 58 秒 |
| 分辨率 | 1920 × 1080（1080p） |
| 编码 | H.264 + AAC（25 fps，立体声） |
| 语言 | 中文（普通话） |

可直接点击上方链接在浏览器中在线预览，或下载后离线观看。

## 内容大纲（9 个分镜）

1. **序 · 刻刀下的色彩传奇** —— 引入蔚县剪纸
2. **技艺 · 名为剪纸，实为刻纸** —— "剪"其实是"刻"，阴刻为主、阳刻为辅
3. **源流 · 从窗花说起** —— 起源于明代，最早形式"天皮亮"
4. **特色 · 三分工，七分染** —— 清代发展出"点彩"技法
5. **工艺 · 一张剪纸的诞生** —— 画样、薰样、刻制、染色、包装
6. **宗师 · 一代宗师王老赏** —— 1890—1951，戏曲人物剪纸大师
7. **非遗 · 走向世界的非遗** —— 2006 国家级非遗，2009 联合国教科文组织
8. **传承 · 刻刀仍在沙沙作响** —— 南张庄村，"中国剪纸第一村"
9. **结语 · 方寸之间，百年色彩**

完整旁白脚本见 [`script.md`](script.md)。

## 目录结构

```
weixian-paper-cutting/
├── video/weixian-paper-cutting.mp4   # 成品视频
├── assets/
│   ├── slides/                       # 每段的分镜图片（PNG，1920×1080）
│   └── audio/                        # 每段旁白音频（MP3）
├── src/
│   ├── segments.json                 # 分镜数据（标题 / 副标题 / 旁白）
│   ├── generate_audio.py             # 生成旁白音频（edge-tts）
│   ├── generate_slides.py            # 生成分镜图片（HTML → Edge 截图）
│   └── build_video.py                # 合成视频（ffmpeg）
├── script.md                         # 旁白脚本
├── LICENSE
└── README.md
```

## 如何重新生成

依赖：Python 3（`edge-tts`）、Microsoft Edge、ffmpeg。

```bash
# 1. 安装 TTS 依赖
py -m pip install edge-tts

# 2. 生成旁白音频
py src/generate_audio.py

# 3. 生成分镜图片
py src/generate_slides.py

# 4. 合成视频（需先修改 build_video.py 中 ffmpeg/ffprobe 的路径）
py src/build_video.py
```

> 说明：`build_video.py` 中 ffmpeg 路径为绝对路径，使用时请改成你本机的 ffmpeg 可执行文件位置。

## 事实依据与参考资料

- 蔚县剪纸起源于明代（单色剪纸），清代发展出"阴刻为主、阳刻为辅"的**点彩剪纸**，俗称"窗花"，素有"三分工、七分染"之说。
- 最早形式为"天皮亮"（在云母薄片上绘图着色）；工艺以刻代剪，含画样、薰样、刻制、染色、包装等工序。
- 王老赏（1890—1951），河北蔚县南张庄村人，蔚县剪纸一代宗师，以戏曲人物见长。
- 2006 年列入首批国家级非物质文化遗产名录；2009 年入选联合国教科文组织"人类非物质文化遗产代表作名录"。
- 南张庄村被誉为"中国剪纸第一村"。

参考链接：

- [剪纸（蔚县剪纸）—— 中国非物质文化遗产网](http://test.nrcca.org.cn/project_details/20184.html)
- [蔚县刻纸 —— Google 艺术与文化](https://artsandculture.google.com/story/QQUx90VL8lM4JA?hl=zh-CN)
- [蔚县剪纸 —— 中国华夏文化遗产基金会](https://www.cchfound.com/product/1095.html#1)
- [王老赏 —— 百度百科](https://wapbaike.baidu.com/item/%E7%8E%8B%E8%80%81%E8%B5%8F/3663612)

## 许可

视频、脚本与分镜图片采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可（署名即可自由使用）；生成脚本（`src/*.py`）采用 [MIT](LICENSE) 许可。

## 免责声明

本视频由 AI 辅助生成，用于教育科普目的。视频中的文字、旁白基于公开资料整理，图片为原创矢量图形，未使用任何受版权保护的剪纸作品照片。
