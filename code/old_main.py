

print("I'm running from the SD card")

if __name__ == '__main__':
    print("running custom function")

    from lights import show
    show()

    from write_data import log_data
    #log_data()