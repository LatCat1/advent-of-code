-- input = "199\n200\n208\n210\n200\n207\n240\n269\n260\n263"

depths :: String -> [Int]
depths = map read . lines

comp :: ([Int] -> Int) -> [Int] -> Int
comp _ [] = 0
comp _ [a] = 0
comp f (a:as) = f (a:as) + comp f as

c1 :: [Int] -> Int
c1 (a:b:as) = if b > a then 1 else 0
c1 _ = 0

c3 :: [Int] -> Int
c3 (a:_:_:d:as) = if d > a then 1 else 0
c3 _ = 0

main :: IO ()
main = do
    file <- readFile "Day1.txt"
    putStrLn $  "Simple: " ++ show (comp c1 $ depths file)
    putStrLn $ "Complex: " ++ show (comp c3 $ depths file)
