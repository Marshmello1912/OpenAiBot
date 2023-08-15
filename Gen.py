import openai

openai.api_key = ''


async def create_text_answer(message: str):

    answer = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo-16k-0613",
                                                 messages=message)

    return answer.choices[0].message.content


async def create_image_answer(message: str):

    answer = await openai.Image.acreate(prompt=message,
                                        n=2,
                                        size="1024x1024")

    return answer.data
