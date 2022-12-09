import Data.List

splitOn :: Eq a => a -> [a] -> [[a]]
splitOn _ [] = [[]]
splitOn x (a:as) = if x == a 
        then []:l:ater
        else (a:l):ater
    where (l:ater) = splitOn x as

solve :: Int -> String -> Int
solve n = sum . take n . reverse . sort . fmap (sum . fmap read) . splitOn "" . splitOn '\n'

day1 :: String -> Int
day1 = solve 1

day2 :: String -> Int
day2 = solve 3

main :: IO ()
main = do
    input <- readFile "Day01.txt"
    print ("Part 1: " ++ (show $ day1 input))
    print ("Part 2: " ++ (show $ day2 input))