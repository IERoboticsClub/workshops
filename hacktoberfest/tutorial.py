users = [
    'velocitatem',
    'haxybaxy'
]

def greet(user):
    print(f'Hello {user}! \n')


if __name__ == "__main__":
    [greet(user) for user in users]
