use std::collections::HashSet;
use std::fs;
use std::time::Instant;

// Step struct
#[derive(Hash, Eq, PartialEq, Debug, Clone)]
struct Step {
    r: i32,
    c: i32,
    d: char,
}

impl Step {
    fn new(r: i32, c: i32, d: char) -> Self {
        Step { r, c, d }
    }
}

// Guard struct
#[derive(Debug)]
struct Guard {
    r: i32,
    c: i32,
    d: char,
    world_map: Vec<Vec<char>>,
    places: Vec<Vec<char>>,
    history: HashSet<Step>,
    map_w: usize,
    map_h: usize,
    leave: bool,
    loop_detected: bool,
}

impl Guard {
    fn new(r: i32, c: i32, d: char) -> Self {
        Guard {
            r,
            c,
            d,
            world_map: vec![],
            places: vec![],
            history: HashSet::new(),
            map_w: 0,
            map_h: 0,
            leave: false,
            loop_detected: false,
        }
    }

    fn parse_map(&mut self, lines: &[&str]) {
        self.world_map = lines.iter().map(|&line| line.chars().collect()).collect();
        self.map_h = self.world_map.len();
        self.map_w = self.world_map[0].len();

        self.places = vec![vec!['.'; self.map_w]; self.map_h];
        for (r, row) in self.world_map.iter().enumerate() {
            for (c, &cell) in row.iter().enumerate() {
                if cell == '^' {
                    self.r = r as i32;
                    self.c = c as i32;
                    self.d = '^';
                    self.places[r][c] = 'X';
                }
            }
        }
    }

    fn make_step(&mut self) {
        if self.leave || self.loop_detected {
            return;
        }

        let direction_map = vec![
            ('^', (-1, 0), '>'),
            ('>', (0, 1), 'V'),
            ('V', (1, 0), '<'),
            ('<', (0, -1), '^'),
        ];

        let (dr, dc, next_d) = direction_map
            .iter()
            .find(|&&(dir, _, _)| dir == self.d)
            .map(|&(_, delta, next_dir)| (delta.0, delta.1, next_dir))
            .unwrap();

        let new_r = self.r + dr;
        let new_c = self.c + dc;

        if new_r < 0 || new_r >= self.map_h as i32 || new_c < 0 || new_c >= self.map_w as i32 {
            self.leave = true;
            return;
        }

        if self.world_map[new_r as usize][new_c as usize] != '#' {
            self.r = new_r;
            self.c = new_c;
            self.places[self.r as usize][self.c as usize] = 'X';
        } else {
            self.d = next_d;
        }

        let current_step = Step::new(self.r, self.c, self.d);
        if self.history.contains(&current_step) {
            self.loop_detected = true;
        } else {
            self.history.insert(current_step);
        }
    }

    fn go(&mut self) -> i32 {
        for _ in 0..100_000 {
            self.make_step();
            if self.leave {
                return 0;
            }
            if self.loop_detected {
                return 1;
            }
        }
        0
    }

    fn print_map(&self) {
        for row in &self.world_map {
            println!("{}", row.iter().collect::<String>());
        }
    }
}

fn get_input(debug: bool) -> String {
    if debug {
        return "....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#..."
            .to_string();
    }
    fs::read_to_string("day6.txt").expect("Failed to read input file")
}

fn silver(input: &str) {
    let lines: Vec<&str> = input.lines().collect();
    let mut guard = Guard::new(0, 0, '^');
    guard.parse_map(&lines);
    guard.go();
    println!("{:?}", guard);
}

fn golden(input: &str) {
    let lines: Vec<&str> = input.lines().collect();
    let mut guard = Guard::new(0, 0, '^');
    guard.parse_map(&lines);
    guard.go();

    let mut tasks: HashSet<(i32, i32)> = HashSet::new();
    for step in &guard.history {
        tasks.insert((step.r, step.c));
    }

    println!("Tasks: {}", tasks.len());

    let mut loop_count = 0;
    let start = Instant::now();

    for (i, task) in tasks.iter().enumerate() {
        if i % 1000 == 0 {
            println!("Processed: {} / {} in {:?}", i, tasks.len(), start.elapsed());
        }

        let mut new_guard = Guard::new(0, 0, '^');
        new_guard.parse_map(&lines);
        new_guard.world_map[task.0 as usize][task.1 as usize] = '#';
        if new_guard.go() == 1 {
            loop_count += 1;
        }
    }

    println!("Total loop count: {}", loop_count);
    println!("Total time: {:?}", start.elapsed());
}

fn main() {
    let input = get_input(false);
    println!("Silver:");
    // silver(&input);
    println!("\nGolden:");
    golden(&input);
}
