type 'a linkedlist = {
  value : 'a ;
  mutable next : 'a linkedlist ref option
}

(* should be an array where array.at(i) is the node with val i + 1, somewhere in the 
   linked list *)
type cuplookup = int linkedlist ref array

let num_cups = 1000000
let cups_str = "389125467"

let modulo a b =
  let rem = a mod b in
  if rem >= 0 then rem else b + rem

let cons_cuplookup str : cuplookup = 
  (* get *)
  let ints = Array.init (String.length str) (String.get str) in
  let mixed_nodes = Array.map (fun x -> ref {value=int_of_char x - int_of_char '1' + 1; next=None}) ints in
  let mixed_nodes_length = Array.length mixed_nodes in
  let all_nodes = Array.init num_cups (fun i -> ref {value=i + 1;next=None}) in
  let _ = Array.blit mixed_nodes 0 all_nodes 0 mixed_nodes_length in
  let option_cuplookup_arr = Array.make num_cups None in
  let _ = Array.mapi (fun i n ->
    !n.next <- Some all_nodes.(modulo (i + 1) num_cups) ;
    option_cuplookup_arr.(!n.value - 1) <- Some n
  ) all_nodes in
  Array.map Option.get option_cuplookup_arr

let cups = cons_cuplookup cups_str

(* let printcups cups =
  let rec helper stop node = 
    if !node.value = 1 && stop then [] else !node.value :: (helper true @@ Option.get !node.next)
  in helper false cups.(0) *)

let pop_next (node : 'a linkedlist ref) : 'a linkedlist ref =
  let next = Option.get !node.next in
  let next_next = Option.get !next.next in
  !node.next <- Some next_next ;
  !next.next <- None ;
  next

let insert_next (node : 'a linkedlist ref) (value : 'a linkedlist ref) : unit =
  let next = Option.get !node.next in
  !node.next <- Some value ;
  !value.next <- Some next ;
  ()

let rec reapply n f x = match n with
  | 0 -> []
  | _ -> f x :: reapply (n-1) f x

let num_moved = 3

let step_cups (cups : cuplookup) (current : int) : int =
  let node = cups.(current - 1) in
  let removed = reapply num_moved pop_next node in
  let destination = List.hd @@ 
    List.filter (fun x -> not @@ List.exists (fun n -> x = !n.value) removed) @@ List.map ((+) 1) @@
    List.map (Fun.flip modulo num_cups) @@ List.map ((-) current) @@ List.tl @@ List.tl @@ List.init (num_moved + 3) Fun.id in 
  let destination_node = cups.(destination - 1) in
  List.iter (insert_next destination_node) removed ;
  !(Option.get !node.next).value

let start_cup : int = 
  String.to_seq cups_str |> List.of_seq |> List.hd |> Char.escaped |> int_of_string

let steps = 10000000

let rec do_repeatedly f= function
  | 0 -> ()
  | n -> f () ;
  (* if n mod 100_000 = 0 then print_endline (string_of_int n) ; *)
  do_repeatedly f (n - 1)

let () = 
  let current = ref start_cup in
  do_repeatedly (fun () -> current.contents <- step_cups cups !current) steps ;
  let cup_1 = cups.(0) in
  let next = Option.get !cup_1.next in
  let nextnext = Option.get !next.next in
  !next.value * !nextnext.value |> string_of_int |> String.cat "Part 2: " |> print_endline
  (* printcups cups |> List.tl |> List.map string_of_int |> String.concat "" |> String.cat "Part 1: " |> print_endline ; *)
  