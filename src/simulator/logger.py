class Logger:
    file_handle = None

    def initialize(file_name):
        try:
            Logger.file_handle = open(file_name,"w")
        except (OSError, IOError) as e:
            print("Error in writing to file " + file_name)
            raise e
    
    def finalize():
        if Logger.file_handle != None:
            Logger.file_handle.close()
        else:
            raise Exception("Logger has not been initialized")

    def add(text):
        if Logger.file_handle != None:
            Logger.file_handle.write(text)
        else:
            #raise Exception("Logger has not been initialized")
            # simply skip
            pass
    
    def add_line(line_text):
        Logger.add(line_text + "\n")

