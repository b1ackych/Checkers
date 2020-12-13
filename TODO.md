# Для идей и тд


# Time

Парадокс?
Мы не можем наперёд посчитать сколько времени у нас уйдет на альфа-бета, т.к. для этого придётся
проанализировать позицию, на что уйдёт время (что и делает альфа-бета).

Вместо этого мы можем сперва просто запустить альфа-бета, и уже потом
прочекать сколько времени у нас ушло на него (и сколько осталось).

Затем, оставшееся время делим на кол-во позиций что нам выдало альфа-бета, и
проверяем каждую позицию такое k времени, что k = оставшееся время / кол-во позиций.
(И, на всякий пожарный можно убрать из k 0,0..1сек)


# Оптимизация ыыы

Я считаю что альфа-бета нужно запускать после каждого нашего хода.
Но, чтобы каждый раз не считать заново позицию каждого нашего хода,
мы можем лучше запомнить его состояние, чтобы сравнивать с новыми возможными ходами.