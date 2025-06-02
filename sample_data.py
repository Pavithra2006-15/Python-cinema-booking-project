"""
Sample data for testing the cinema booking platform
"""

SAMPLE_MOVIES = [
    {
        'title': 'Avengers: Endgame',
        'description': 'The epic conclusion to the Infinity Saga that became a defining moment in cinematic history.',
        'duration': 181,
        'release_date': '2023-12-01',
        'certification': 'UA',
        'status': 'now_showing',
        'director': 'Anthony Russo, Joe Russo',
        'cast': ['Robert Downey Jr.', 'Chris Evans', 'Mark Ruffalo', 'Chris Hemsworth'],
        'imdb_rating': 8.4,
        'average_rating': 4.5,
        'total_reviews': 1250,
        'genres': ['Action', 'Adventure', 'Drama'],
        'languages': ['English', 'Hindi']
    },
    {
        'title': 'Spider-Man: No Way Home',
        'description': 'Peter Parker seeks help from Doctor Strange when his secret identity is revealed.',
        'duration': 148,
        'release_date': '2023-11-15',
        'certification': 'UA',
        'status': 'now_showing',
        'director': 'Jon Watts',
        'cast': ['Tom Holland', 'Zendaya', 'Benedict Cumberbatch', 'Jacob Batalon'],
        'imdb_rating': 8.2,
        'average_rating': 4.2,
        'total_reviews': 980,
        'genres': ['Action', 'Adventure', 'Sci-Fi'],
        'languages': ['English', 'Hindi', 'Tamil']
    },
    {
        'title': 'The Batman',
        'description': 'Batman ventures into Gotham City\'s underworld when a sadistic killer leaves behind a trail of cryptic clues.',
        'duration': 176,
        'release_date': '2023-10-20',
        'certification': 'UA',
        'status': 'now_showing',
        'director': 'Matt Reeves',
        'cast': ['Robert Pattinson', 'Zoë Kravitz', 'Paul Dano', 'Jeffrey Wright'],
        'imdb_rating': 7.8,
        'average_rating': 4.8,
        'total_reviews': 756,
        'genres': ['Action', 'Crime', 'Drama'],
        'languages': ['English', 'Hindi']
    },
    {
        'title': 'Top Gun: Maverick',
        'description': 'After thirty years, Maverick is still pushing the envelope as a top naval aviator.',
        'duration': 130,
        'release_date': '2023-09-10',
        'certification': 'UA',
        'status': 'now_showing',
        'director': 'Joseph Kosinski',
        'cast': ['Tom Cruise', 'Miles Teller', 'Jennifer Connelly', 'Jon Hamm'],
        'imdb_rating': 8.3,
        'average_rating': 4.3,
        'total_reviews': 892,
        'genres': ['Action', 'Drama'],
        'languages': ['English', 'Hindi']
    },
    {
        'title': 'Dune: Part Two',
        'description': 'Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators.',
        'duration': 166,
        'release_date': '2024-01-15',
        'certification': 'UA',
        'status': 'coming_soon',
        'director': 'Denis Villeneuve',
        'cast': ['Timothée Chalamet', 'Zendaya', 'Rebecca Ferguson', 'Oscar Isaac'],
        'imdb_rating': 8.9,
        'average_rating': 4.7,
        'total_reviews': 234,
        'genres': ['Action', 'Adventure', 'Drama'],
        'languages': ['English', 'Hindi']
    }
]

SAMPLE_THEATRES = [
    {
        'name': 'PVR Cinemas - Phoenix Mall',
        'city': 'Mumbai',
        'address': 'Phoenix Mills Compound, High Street Phoenix, Lower Parel',
        'phone_number': '+91-22-6671-7777',
        'facilities': ['Parking', 'Food Court', 'ATM', 'Wheelchair Access'],
        'screens': [
            {
                'name': 'Screen 1',
                'screen_type': 'imax',
                'total_seats': 300,
                'sound_system': 'Dolby Atmos'
            },
            {
                'name': 'Screen 2',
                'screen_type': '3d',
                'total_seats': 250,
                'sound_system': 'DTS'
            }
        ]
    },
    {
        'name': 'INOX - Forum Mall',
        'city': 'Bangalore',
        'address': '21, Hosur Road, Koramangala',
        'phone_number': '+91-80-4112-4444',
        'facilities': ['Parking', 'Food Court', 'Gaming Zone'],
        'screens': [
            {
                'name': 'Screen 1',
                'screen_type': '2d',
                'total_seats': 200,
                'sound_system': 'Dolby Digital'
            }
        ]
    }
]
