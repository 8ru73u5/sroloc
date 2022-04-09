# SROLOC

Are you tired of white text on a black background? Maybe you've been experimenting with the `curses` library or using
raw escape sequences to print something colorful to the terminal? Well, perhaps I'm not gonna convince you to start
using `sroloc` all of a sudden, but you have to admit that every Python library designed to simplify using colors in the
terminal does that job very poorly:

```python
import curses

screen = curses.initscr()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
screen.addstr('This is so ')
screen.addstr('cringe', curses.color_pair(1))
screen.addstr('...')
```

Really? So maybe like that:

```python
print('This is even more \x1b[31mcringe\x1b[0m...')
```

Or maybe just use `colorama`? Nah, we don't talk about `colorama` in this repo. Look at this graph:

```python
from sroloc import ColorSegment as c

print(f'This is not {c("cringe"):red} at all!')
```

And you can't get simpler than that! Well... you can, but you'd probably have to modify Python internals to
change `str.__format__` so you could omit this `c("")` thing entirely. It may be possible in the future, but right now
we're stuck with using `sroloc` unfortunately...

Now, fasten your seatbelts ladies and gentlemen because we're just getting started!

## Color support

Here's a nice table:

| Class                  |  Bits per color  |
|------------------------|:----------------:|
| `BasicColor` (default) |        3         |
| `ExtendedColor`        |        8         |
| `TrueColor`            |        24        |

Please note that some terminals might not support one of more of those. Check your `terminfo` or your terminal manual
before complaining.

Here are some examples:

```python
from sroloc import ColorSegment
from sroloc.color import BasicColor, ExtendedColor, TrueColor

colorful = ColorSegment('colorful')

# BasicColor (aka ANSI 3-bit color)
ColorSegment.set_color_scheme(BasicColor)  # This can be omitted as it's the default one
print(f'I am {colorful:blue}!')

# ExtendedColor (aka ANSI-256 color)
ColorSegment.set_color_scheme(ExtendedColor)
print(f'I am {colorful:hot_pink}!')

# TrueColor
ColorSegment.set_color_scheme(TrueColor)
print(f'I am {colorful:#6ae5e8}!')
```

## Foreground and background

Of course, you can specify the background color as well. Just separate it from the foreground color using separator,
which is set to `/` by default:

```python
print(f'I have a {c("background"):red/cyan} color as well!')
```

If you want to only set the background color without messing with the default foreground color, use a color
placeholder (default: `_`) instead of specifying color name like so:

```python
print(f'Who cares about foreground {c("color"):_/red} anyway...')
```

You can specify more than one color but only the last one will be applied:

```python
# This will print black text on a yellow background:
print(f'No color {c("mixing"):red blue/green _/yellow black} on my watch!')
```

## Modifiers

You can also provide some modifiers if you want to spice things up a little bit:

```python
# Full form
print(f'This is a {c("mistake"):bold strikethrough red}.')

# Shorthand form
print(f'This is a {c("mistake"):b s red}.')
```

There are two types of modifiers: **color** and **text**. The difference is that you can mix text modifiers, but you can
only have one color modifier applied at once. There are only 3 color modifiers: bold, faint and reset. I think it's
pretty obvious why you cannot mix them. On the other hand, text modifiers can stack on top of each other in any
combination possible. Those are the most common ones: _italic_, <u>underline</u>, ~~strikethrough~~.

Every terminal has its own set of supported text modifiers so please check `terminfo` before rage-quitting when your
code doesn't seem to work.

## Custom color schemes

If you want to use your own custom set of colors, you can do this very easily like so:

```python
from sroloc.color import TrueColor

monokai_colors = {
    'white': '#d6d6d6',
    'yellow': '#e5b567',
    'green': '#b4d273',
    'orange': '#e87d3e',
    'purple': '#9e86c8',
    'pink': '#b05279',
    'blue': '#6c99bb'
}


class MonokaiTheme(TrueColor):
    pass


for name, value in monokai_colors.items():
    MonokaiTheme.add_hex_color_to_bank(name, value)
```

And now you're ready to go:

```python
c.set_color_scheme(MonokaiTheme)

print(f'I am using a {c("Monokai"):green} {c("color"):pink} {c("theme"):blue}!')
```

## Disclaimer

This library only works on terminals
where [ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code#DOS,_OS/2,_and_Windows) work without any
additional setup. This means that it wouldn't work for example on Windows cmd.

I want to keep `sroloc` relatively simple and without any dependencies, so don't expect any crazy new features in the
future. I'll keep updating this readme and maybe even consider creating a wiki page. Right now it doesn't make sense
because nobody is going to read it anyway...
