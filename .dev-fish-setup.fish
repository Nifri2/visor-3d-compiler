# .dev-fish-setup.fish

function fish_greeting
    echo "Proto Dev Environment loaded :3"
end

function sync
    rshell -p /dev/ttyACM0 rsync . /pyboard/
end

function runpy
    rshell -p /dev/ttyACM0 cp main.py /pyboard/main.py
    rshell -p /dev/ttyACM0 repl "~ import main"
end
