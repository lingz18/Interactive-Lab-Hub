while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 

    ### render snowflake
    if buttonA.value and buttonB.value:
        font = getFont(18)
        offset_x = 1
        offset_y = 1
        for i in range(10):
            draw.text((x[i], y[i]), "❄", font=font, fill="#0000FF")
            x[i] = x[i] + offset_x if x[i] + offset_x < width else x[i] + offset_x - width
            y[i] = y[i] + offset_y if y[i] + offset_y < height else y[i] + offset_y - height
        reset = True
    elif not buttonA.value and buttonB.value:
        offset_x = 2
        offset_y = 6
        for i in range(10):
            draw.text((x[i], y[i]), "\\", font=font, fill="#BFE7F6")
            x[i] = x[i] + offset_x if x[i] + offset_x < width else x[i] + offset_x - width
            y[i] = y[i] + offset_y if y[i] + offset_y < height else y[i] + offset_y - height
        reset = True
    elif buttonA.value and not buttonB.value:
        offset_x = random.randint(-1, high=1, size=10)
        offset_y = random.randint(5, size=10)
        offset_y = -offset_y
        if reset:
            x1, y1 = getRandomXY()
        for i in range(10):
            draw.text((x[i], y[i]), "❄", font=font, fill="#0000FF")
            draw.text((x1[i], y1[i]), ".", font=font, fill="#0000FF")
            x[i] = x[i] + offset_x[i] if x[i] + offset_x[i] < width else x[i] + offset_x[i] - width
            y[i] = y[i] + offset_y[i] if y[i] + offset_y[i] < height else y[i] + offset_y[i] - height
            x1[i] = x1[i] + offset_x[i] if x1[i] + offset_x[i] < width else x1[i] + offset_x[i] - width
            y1[i] = y1[i] + offset_y[i] if y1[i] + offset_y[i] < height else y1[i] + offset_y[i] - height
        reset = False

    ### render clock
    date = strftime("%m/%d/%Y")
    timer = strftime("%H:%M:%S")
    font = getFont(44)
    
    x_1 = width/2 - font.getsize(timer)[0]/2
    y_1 = height/2 - font.getsize(timer)[1]/2
    draw.text((x_1, y_1), timer, font=font, fill="#FFFFFF")

    font = getFont(18)
    x_2 = width/2 - font.getsize(date)[0]/2
    y_1 -= font.getsize(date)[1]
    draw.text((x_2, y_1), date, font=font, fill="#FFFFFF")
    # Display image.
    disp.image(image, rotation)
    time.sleep(0.001)