from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime

# Iterator interface
class Iterator(ABC):
    @abstractmethod
    def next(self) -> Optional[object]:
        pass
    
    @abstractmethod
    def has_next(self) -> bool:
        pass

# Concrete Iterators
class PlaylistIterator(Iterator):
    def __init__(self, songs: List[str]):
        self._songs = songs
        self._position = 0
        
    def next(self) -> Optional[str]:
        if self.has_next():
            song = self._songs[self._position]
            self._position += 1
            return song
        return None
    
    def has_next(self) -> bool:
        return self._position < len(self._songs)

class BookshelfIterator(Iterator):
    def __init__(self, books: List[Dict]):
        self._books = books
        self._position = 0
    
    def next(self) -> Optional[Dict]:
        if self.has_next():
            book = self._books[self._position]
            self._position += 1
            return book
        return None
    
    def has_next(self) -> bool:
        return self._position < len(self._books)

class TaskQueueIterator(Iterator):
    def __init__(self, tasks: List[Dict]):
        self._tasks = sorted(tasks, key=lambda x: x['priority'])
        self._position = 0
    
    def next(self) -> Optional[Dict]:
        if self.has_next():
            task = self._tasks[self._position]
            self._position += 1
            return task
        return None
    
    def has_next(self) -> bool:
        return self._position < len(self._tasks)

# Collection interface
class Collection(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass

# Concrete Collections
class MusicPlaylist(Collection):
    def __init__(self):
        self._songs: List[str] = []
    
    def add_song(self, song: str) -> None:
        self._songs.append(song)
    
    def create_iterator(self) -> Iterator:
        return PlaylistIterator(self._songs)

class Bookshelf(Collection):
    def __init__(self):
        self._books: List[Dict] = []
    
    def add_book(self, title: str, author: str, year: int) -> None:
        self._books.append({
            'title': title,
            'author': author,
            'year': year
        })
    
    def create_iterator(self) -> Iterator:
        return BookshelfIterator(self._books)

class TaskQueue(Collection):
    def __init__(self):
        self._tasks: List[Dict] = []
    
    def add_task(self, description: str, priority: int, deadline: datetime) -> None:
        self._tasks.append({
            'description': description,
            'priority': priority,
            'deadline': deadline
        })
    
    def create_iterator(self) -> Iterator:
        return TaskQueueIterator(self._tasks)

# Usage example
def main():
    # Music Playlist Example
    playlist = MusicPlaylist()
    playlist.add_song("Shape of You")
    playlist.add_song("Blinding Lights")
    playlist.add_song("Stay")
    
    print("Playing songs:")
    iterator = playlist.create_iterator()
    while iterator.has_next():
        print(f"🎵 {iterator.next()}")
    
    # Bookshelf Example
    bookshelf = Bookshelf()
    bookshelf.add_book("The Pragmatic Programmer", "Dave Thomas", 1999)
    bookshelf.add_book("Clean Code", "Robert Martin", 2008)
    bookshelf.add_book("Design Patterns", "Gang of Four", 1994)
    
    print("\nBooks in shelf:")
    iterator = bookshelf.create_iterator()
    while iterator.has_next():
        book = iterator.next()
        print(f"📚 {book['title']} by {book['author']} ({book['year']})")
    
    # Task Queue Example
    task_queue = TaskQueue()
    task_queue.add_task("Fix critical bug", 1, datetime(2024, 12, 24))
    task_queue.add_task("Update documentation", 3, datetime(2024, 12, 26))
    task_queue.add_task("Deploy new feature", 2, datetime(2024, 12, 25))
    
    print("\nTasks by priority:")
    iterator = task_queue.create_iterator()
    while iterator.has_next():
        task = iterator.next()
        print(f"📋 Priority {task['priority']}: {task['description']} (Due: {task['deadline'].date()})")

if __name__ == "__main__":
    main()