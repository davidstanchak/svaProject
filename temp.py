
        for row in range(NUM_ROWS):
            row_aliens = aliens_by_row[row]

            for a in row_aliens:
                a.update()
                a.draw(screen)

            #remove aliens that moved off screen
            aliens_by_row[row] = [a for a in row_aliens if not a.is_off_screen()] 
            


        #randomized spawning logic
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            random_row = random.randint(0, NUM_ROWS - 1)
            row_aliens = aliens_by_row[random_row]

            if not row_aliens or row_aliens[-1].x < SCREEN_WIDTH - random.randint(CELL_WIDTH, CELL_WIDTH * 3):
                aliens_by_row[random_row].append(alien(random_row, CELL_WIDTH, CELL_HEIGHT, GRID_LEFT_X, GRID_TOP_Y))
                
                
                
                
                
                
                
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS): 
                cell_color = (183, 98, 45) if (row + col) % 2 == 0 else (213, 128, 75)
                #calling function to draw AND round all individual grid squares.
                draw_rounded_rect(
                    screen,
                    cell_color,
                    (
                        GRID_LEFT_X + col * CELL_WIDTH, #each grid square is placed
                        GRID_TOP_Y + row * CELL_HEIGHT, 
                        CELL_WIDTH + 7,  #stationary width and height
                        CELL_HEIGHT
                    ),
                    radius=5
                )
                
                

        draw_rounded_rect(
            screen,
            (213, 128, 75), 
            (GRID_LEFT_X, GRID_TOP_Y, GRID_WIDTH, GRID_HEIGHT),
            radius=5
        )



        #calling function to draw AND round a shop rectangle
        draw_rounded_rect(
            screen,
            "#5d2285",
            (margin_sides, 12.5, 550, 145),
            radius=10
        )
        