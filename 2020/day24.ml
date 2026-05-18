

(* hexagonal directions *)
type dir = | NE | NW | E | W | SE | SW
(* hexagonal location (x, y) *)
type hexloc = int * int

let all_dirs = [NE;NW;E;W;SE;SW]

let move (x, y) = function
  | NE -> (x, y+1)
  | SW -> (x, y-1)
  | NW -> (x-1, y+1)
  | SE -> (x+1, y-1)
  | E -> (x+1, y)
  | W -> (x-1, y)

let all_adj (l : hexloc) = List.map (move l) all_dirs

let origin : hexloc = (0, 0)
let path_end = List.fold_left move origin

let read_all_lines file : string Seq.t =
  let read_line_helper () = (
    try Some (input_line file)
    with End_of_file -> None
  ) in
  Seq.forever read_line_helper |> Seq.take_while Option.is_some |> Seq.map Option.get

exception Parse_fail
let rec parse_directions = function
    | 'n' :: 'e' :: ds -> NE :: parse_directions ds
    | 'n' :: 'w' :: ds -> NW :: parse_directions ds
    | 's' :: 'e' :: ds -> SE :: parse_directions ds
    | 's' :: 'w' :: ds -> SW :: parse_directions ds
    | 'e' :: ds        -> E  :: parse_directions ds
    | 'w' :: ds        -> W  :: parse_directions ds
    | [] -> []
    | _ -> raise Parse_fail

let parse_line_to_dirs line = parse_directions @@ List.of_seq @@ String.to_seq line

module HexlocSet = Set.Make(struct
  type t = hexloc
  let compare = Pair.compare compare compare
end)

let fliploc set loc = if HexlocSet.mem loc set then HexlocSet.remove loc set else HexlocSet.add loc set

let adjacent_count set loc = loc |> all_adj |> List.filter (Fun.flip HexlocSet.mem set) |>
  List.fold_left (Fun.flip (Fun.const ((+) 1))) 0

let step_day (black_tiles: HexlocSet.t) =
  let white_tiles_to_check = black_tiles
    |> HexlocSet.to_list
    |> List.concat_map all_adj
    |> HexlocSet.of_list
    |> Fun.flip HexlocSet.diff black_tiles in
  let black_tiles_remaining = black_tiles
    |> HexlocSet.filter (fun t -> List.exists ((=) @@ (adjacent_count black_tiles t)) [1;2]) in
  let white_tiles_flip = white_tiles_to_check
    |> HexlocSet.filter (fun t -> List.exists ((=) @@ (adjacent_count black_tiles t)) [2]) in
  HexlocSet.union black_tiles_remaining white_tiles_flip

let gen_tileset_seq = Seq.unfold (fun t ->
    let next_day = step_day t in
    Some (next_day, next_day))

(* 1-indexed *)
let seq_nth seq n = Seq.drop (n - 1) seq |> Seq.take 1 |> List.of_seq |> List.hd

let size set = HexlocSet.fold (Fun.const ((+) 1)) set 0

let () = 
  let args = Sys.argv in
  if Array.length args != 3
    then print_endline "Proper usage: ./day24.exe [target file] [num_days]" else
  let file_name = args.(1) in
  let num_days = int_of_string args.(2) in
  let file_in = open_in file_name in
  try
    let lines = read_all_lines file_in in
    let all_dirs = Seq.map parse_line_to_dirs lines in
    let flipped_tiles = Seq.fold_left fliploc HexlocSet.empty @@ Seq.map path_end all_dirs in
    print_endline @@ "P1: " ^ string_of_int @@ size flipped_tiles ;
    let tile_seq = gen_tileset_seq flipped_tiles in
    print_endline @@ "P2: " ^ string_of_int @@ size @@ seq_nth tile_seq num_days ;
    close_in file_in
  with e -> 
    close_in_noerr file_in ;
    raise e