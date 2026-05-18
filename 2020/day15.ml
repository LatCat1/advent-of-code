

module IntHashtbl = Hashtbl.Make(Int)

(* let print_hashtbl tbl =
  IntHashtbl.to_seq tbl
  |> List.of_seq
  |> List.map (fun (k, (v1, v2)) -> string_of_int k ^ ": (" ^ string_of_int v1 ^ ", " ^ string_of_int v2 ^ ")")
  |> String.concat ", "
  |> String.cat "Table: "
  |> print_endline *)


type said_history = (int * int) IntHashtbl.t

let say_number (num_to_say : int) (history : said_history) (step : int) : unit =
  (* print_endline @@ "Saying " ^ string_of_int num_to_say ^ "on turn " ^ string_of_int (step + 1) ; *)
  if IntHashtbl.mem history num_to_say
    then IntHashtbl.replace history num_to_say (step, fst @@ IntHashtbl.find history num_to_say) 
    else IntHashtbl.add     history num_to_say (step, step) ;
  ()

let game_seq (starting : int list) = 
  let history = IntHashtbl.create 1_000_000 in
  let step = ref (-1) in
  let last_said = ref (-1) in
  let starting_length = List.length starting in
  let f () = 
    step.contents <- !step + 1 ;
    if !step < starting_length
    then (
      say_number (List.nth starting !step) history !step;
      last_said.contents <- (List.nth starting !step))
    else (
      (* figure out which number to say *)
      last_said.contents <- (fun (a, b) -> (a - b)) @@ Option.value (IntHashtbl.find_opt history !last_said) ~default:(0, 0) ;
      say_number !last_said history !step
    ) ;
    (* print_endline @@ "Turn " ^ string_of_int !step ^ " said " ^ string_of_int !last_said ;
    print_hashtbl history ; *)
    (* if !step mod 10_000 = 0 then *)
      (* print_endline @@ string_of_int !step; *)
    !last_said
  in
  Seq.forever f 

let total_steps_p1 = 2020
let total_steps_p2 = 30_000_000

let said_on start (num_steps) = game_seq start |> (Seq.drop @@ num_steps - 1) |> Seq.take 1 |> List.of_seq |> List.hd

let () = 
  let init = Sys.argv.(1) in

  let start = init
    |> String.split_on_char ',' 
    |> List.map int_of_string in

  let said_p1 = said_on start total_steps_p1 in
  print_endline @@ "P1: " ^ string_of_int said_p1 ;

  let said_p2 = said_on start total_steps_p2 in
  print_endline @@ "P2: " ^ string_of_int said_p2 ;