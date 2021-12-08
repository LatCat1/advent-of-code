splitOn :: (a -> Bool) -> [a] -> [[a]]
splitOn f [] = []
splitOn f as
    | null r    = [l]
    | otherwise = l : splitOn f (tail r)
    where (l,r) = break f as

parseLocs :: String -> [Int]
parseLocs = map read . splitOn (== ',')

dist1 :: Int -> Int -> Int
dist1 a b = abs (a-b)

dist2 :: Int -> Int -> Int
dist2 a b = n*(n+1) `div` 2
    where n = abs (a-b)

locsToFuel :: (Int -> Int -> Int) -> [Int] -> [Int]
locsToFuel d ls = map (sum . flip map ls . d) ls

day1 :: [Int] -> Int
day1 = minimum . locsToFuel dist1

day2 :: [Int] -> Int
day2 = minimum . locsToFuel dist2

main :: IO ()
main = do
    locs <- parseLocs . head . lines <$> readFile "Day7.txt"
    putStrLn $ "Part 1: " ++ show (day1 locs)
    putStrLn $ "Part 2: " ++ show (day2 locs)
