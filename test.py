

def shutdown():
    print('shutdown')
    def finalize():
        print('finalize')

if __name__ == '__main__':
    shutdown()