locations = [
    {
        "id": 0,
        "name": "Dorian Jail Cell",
        "connections": [1],
        "details": [
            {
                "id": 0,
                "lv": 1,
                "dt": "small, cramped cell"
            },
            {
                "id": 1,
                "lv": 1,
                "dt": "small window with bars on the back wall of the cell, leading to the outside"
            },
            {
                "id": 2,
                "lv": 1,
                "dt": "small bed"
            },
            {
                "id": 3,
                "lv": 1,
                "dt": "small, wooden table and chair"
            },
            {
                "id": 4,
                "lv": 1,
                "dt": "the door is iron and has a small window with bars"    
            },
            {
                "id": 5, 
                "lv": 2, 
                "dt": "a crack in one of the cobbled stone tiles on the floor"
            },
            {
                "id": 6, 
                "lv": 2, 
                "dt": "a leak in the ceiling drips occasionally onto the floor - right above the crack in the stone"
            }, 
            {
                "id": 7, 
                "lv": 3, 
                "dt": "the padlock on the cell door is a bit rusty"
            },
            {
                "id": 8, 
                "lv": 4, 
                "dt": "you hear crows cawing outside the window"
            },
            {
                "id": 9, 
                "lv": 5, 
                "dt": "you hear wind whistling through tree leaves outside the window"
            }
        ]
    },
    {
        "id": 1,
        "name": "Prison Courtyard",
        "connections": [0],
        "details": [
            {
                "id": 0,
                "lv": 1,
                "dt": "open courtyard surrounded by high stone walls"
            },
            {
                "id": 1,
                "lv": 1,
                "dt": "guard tower in each corner of the courtyard"
            },
            {
                "id": 2,
                "lv": 1,
                "dt": "wooden benches scattered around"
            },
            {
                "id": 3,
                "lv": 2,
                "dt": "overgrown weeds pushing through cracks in the stone floor"
            },
            {
                "id": 4,
                "lv": 2,
                "dt": "a rusty water pump in the center"
            },
            {
                "id": 5,
                "lv": 3,
                "dt": "one of the guard towers appears to be unmanned"
            },
            {
                "id": 6,
                "lv": 3,
                "dt": "pile of old crates near the eastern wall"
            },
            {
                "id": 7,
                "lv": 4,
                "dt": "the crates seem to be arranged in a way that could provide cover"
            },
            {
                "id": 8,
                "lv": 4,
                "dt": "guards seem to patrol in predictable patterns"
            },
            {
                "id": 9,
                "lv": 5,
                "dt": "there's a section of the wall where the mortar between stones has significantly eroded"
            }
        ]
    }
]


def get_details(location_id: int, perception: int) -> object: 
    return {
        "name": locations[location_id]["name"],
        "details": [detail["dt"] for detail in sorted(locations[location_id]["details"], key=lambda x: -x["lv"]) if detail["lv"] <= perception]
    }