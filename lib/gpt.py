import openai

def get_gpt_response(prompt, print_stream = False, print_func=None, model='gpt-4', temperature = 0):
    def _print_func(x):
        print_func(x) if print_func else print(x, end='')

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        stream= True if print_stream == True else False
    )

    if (print_stream):
        for chunk in response:
            content = chunk.choices[0].delta.get("content", '')
            _print_func(content)
            whole_message+=content

    return response.choices[0].message.content

def get_gpt_chat_response(messages, print_stream = False, print_func=None, model='gpt-4', temperature = 0):
    def _print_func(x):
        print_func(x) if print_func else print(x, end='')

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream= True if print_stream == True else False
    )

    whole_message= ''

    if (print_stream):
        for chunk in response:
            content = chunk.choices[0].delta.get("content", '')
            _print_func(content)
            whole_message+=content

    return whole_message if print_stream == True else response.choices[0].message.content
