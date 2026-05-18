let read_all_lines file : string Seq.t =
  let read_line_helper () = (
    try Some (input_line file)
    with End_of_file -> None
  ) in
  Seq.forever read_line_helper |> Seq.take_while Option.is_some |> Seq.map Option.get

(* [discrete_log b m n] is x, such that assumes that log_b(x) = n (mod m). This
   is always solvable when b and p are coprime, and may be solvable otherwise *)

let modulus = 20201227
let base = 7

let discrete_log (b : int) (m : int) (n : int) =
  let rec dlog_helper x c = if x = n then c else dlog_helper ((x * b) mod m) (c+1) in
  dlog_helper 1 0

let transform subject loops = 
  let rec transform_helper value = function
    | 0 -> value
    | n -> transform_helper ((value * subject) mod modulus) (n - 1)
  in transform_helper 1 loops

let () = 
  let args = Sys.argv in
  if Array.length args <> 2 then print_endline "Useage: ./day25.exe [input_file_path]" else
  let file_name = args.(1) in
  let file_in = open_in file_name in
  try
    let lines = read_all_lines file_in in
    let keys_list = List.of_seq @@ Seq.map int_of_string lines in
    let key1 = List.nth keys_list 0 in
    let key2 = List.nth keys_list 1 in
    let key1_loops = discrete_log base modulus key1 in
    let encryption_key = transform key2 key1_loops in
    print_endline @@ "P1: " ^ string_of_int encryption_key ;
    close_in file_in
  with e -> 
    close_in_noerr file_in ;
    raise e
