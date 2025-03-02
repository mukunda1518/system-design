import datetime
import itertools
from enum import Enum



class SeatType(Enum):
    NORMAL = "Normal"
    PREMIUM = "Premium"

class SeatStatus(Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"

class BookingStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"


class User:
    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

class Movie:
    def __init__(self, id: str, title: str, description: str, duration: int):
        self.id = id
        self.title = title
        self.description = description
        self.duration_in_min = duration

class Seat:
    def __init__(self, id: str, row: int, column: int, seat_type: SeatType, price: float, seat_status: SeatStatus):
        self.id = id
        self.row = row
        self.column = column
        self.seat_type = seat_type
        self.price = price
        self.status = seat_status

class Show:
    def __init__(self, id: str, movie: Movie, theater: 'Theater', start_datetime: datetime.datetime, end_datetime: datetime.datetime, seats: dict[str, Seat]):
        self.id = id
        self.movie = movie
        self.theater = theater
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.seats = seats

class Theater:
    def __init__(self, id: str, name: str, location: str, shows: list[Show]):
        self.id = id
        self.name = name
        self.location = location
        self.shows = shows

class Booking:
    def __init__(self, id: str, user: User, show: Show, seats: list[Seat], total_price: float, status: BookingStatus, timestamp: datetime.datetime):
        self.id = id
        self.user = user
        self.show = show
        self.seats = seats
        self.total_price = total_price
        self.status = status
        self.timestamp = timestamp

class MovieTicketBookingSystem:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.movies = []
            cls._instance.theaters = []
            cls._instance.shows = {}
            cls._instance.bookings = {}
            cls._instance.booking_counter = itertools.count(1)
        return cls._instance


    @staticmethod
    def get_instance():
        if MovieTicketBookingSystem._instance is None:
            MovieTicketBookingSystem()
        return MovieTicketBookingSystem._instance

    def add_movie(self, movie: Movie):
        self.movies.append(movie)

    def add_theater(self, theater: Theater):
        self.theaters.append(theater)

    def add_show(self, show: Show):
        self.shows[show.id] = show

    def get_movies(self) -> list[Movie]:
        return self.movies

    def get_theaters(self) -> list[Theater]:
        return self.theaters

    def get_shows(self) -> list[Show]:
        return self.shows

    def get_show(self, show_id: str) -> Show:
        return self.shows.get(show_id)

    def book_tickets(self, user: User, show: Show, selected_seats: list[Seat]) -> Booking:
        if self._are_seats_available(show, selected_seats):
            self._mark_seats_as_booked(show, selected_seats)
            total_price = self._calculate_total_price(selected_seats)
            booking_id = self._generate_booking_id()
            booking = Booking(booking_id, user, show, selected_seats, total_price, BookingStatus.PENDING, datetime.datetime.now())
            self.bookings[booking_id] = booking
            return booking

    def _are_seats_available(self, show: Show, selected_seats: list[Seat]) -> bool:
        for seat in selected_seats:
            show_seat = show.seats.get(seat.id)
            if show_seat is None or show_seat.status != SeatStatus.AVAILABLE:
                return False
        return True

    def _mark_seats_as_booked(self, show, selected_seats):
        for seat in selected_seats:
            show_seat = show.seats.get(seat.id)
            show_seat.status = SeatStatus.BOOKED
     
    def _calculate_total_price(self, selected_seats: list[Seat]) -> float:
        return sum(seat.price for seat in selected_seats)

    def _generate_booking_id(self):
        booking_number = next(self.booking_counter)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BKG{timestamp}{booking_number:06d}"

    def confirm_booking(self, booking_id: str) -> bool:
        booking = self.bookings.get(booking_id)
        if booking and booking.status == BookingStatus.PENDING:
            booking.status = BookingStatus.CONFIRMED
            # Process payment and send notification
            # ...

    def cancel_booking(self, booking_id: str) -> bool:
        booking = self.bookings.get(booking_id)
        if booking and booking.status == BookingStatus.PENDING:
            booking.status = BookingStatus.CANCELLED
            self._mark_seats_as_available(booking.show, booking.seats)
            # Process refund and send cancellation notification
            # ....

    def _mark_seats_as_available(self, show: Show, selected_seats: list[Seat]):
        for seat in selected_seats:
            show_seat = show.get(seat.id)
            show_seat.status = SeatStatus.AVAILABLE


class MovieTicketBookingDemo:
    
    @staticmethod
    def run():
        booking_system = MovieTicketBookingSystem.get_instance()
        
        # Add Movies
        movie1 = Movie("M1", "Avengers: Endgame", "Superhero movie by Marvel", 180)
        movie2 = Movie("M2", "Joker", "Psychological thriller", 122)
        movie3 = Movie("M3", "Tenet", "Sci-fi action thriller", 150)
        booking_system.add_movie(movie1)
        booking_system.add_movie(movie2)
        booking_system.add_movie(movie3)

        # Add Theaters
        pvr = Theater("T1", "PVR Cinemas", "Downtown", [])
        inox = Theater("T2", "INOX", "Uptown Mall", [])
        booking_system.add_theater(pvr)
        booking_system.add_theater(inox)

        # Add Shows
        today = datetime.datetime.now()
        avengers_show = Show("S1", movie1, pvr, today, today + datetime.timedelta(minutes=movie1.duration_in_min), create_seats(10, 10))
        joker_show = Show("S2", movie2, pvr, today, today + datetime.timedelta(minutes=movie2.duration_in_min), create_seats(8, 8))
        booking_system.add_show(avengers_show)
        booking_system.add_show(joker_show)
    
        # Book Tickets
        user = User("U1", "John Doe", "john@example.com")
        selected_seats = [avengers_show.seats["1-5"], avengers_show.seats["1-6"]]
        booking = booking_system.book_tickets(user, avengers_show, selected_seats)
        if booking:
            print(f"Ticket booking successful. Booking ID: {booking.id}")
            booking_system.confirm_booking(booking.id)
        else:
            print("Booking Failed. Seats not available")

def create_seats(rows: int, columns: int):
    seats = {}
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            seat_id = f"{row}-{col}"
            seat_type = SeatType.NORMAL if row <= 3 else SeatType.PREMIUM
            price = 200 if seat_type == SeatType.NORMAL else 300
            seat = Seat(seat_id, row, col, seat_type, price, SeatStatus.AVAILABLE)
            seats[seat_id] = seat
    return seats
    

if __name__ == "__main__":
    MovieTicketBookingDemo.run()