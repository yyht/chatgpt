

prompt_template = """
Act as the author and provide exactly 2 bullet points for the text transcript given in the format [seconds] - [text] \nMake sure that:\n    - Please start by summarizing the whole video in one short sentence\n    - Then, please summarize with each bullet_point is at most 32 words\n    - each bullet_point start with \"- \" or a number or a bullet point symbol\n    - each bullet_point should has the start timestamp, use this template: - seconds -[bullet_point]\n    - there may be typos in the subtitles, please correct them\n    - Reply all in Chinese Language.
视频ASR: {}
"""

