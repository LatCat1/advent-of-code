
data FishTracker = FT Int Int Int Int Int Int Int Int Int

advanceDay :: FishTracker -> FishTracker
advanceDay (FT a b c d e f g h i) = FT b c d e f g (a+h) i a

{- this is horrifically ugly, should use a better representation for tracking fish -}
initTracker :: [Int] -> FishTracker
initTracker = foldr recurse (FT 0 0 0 0 0 0 0 0 0)
    where recurse 0 (FT a b c d e f g h i) = FT (a+1) b c d e f g h i
          recurse 1 (FT a b c d e f g h i) = FT a (b+1) c d e f g h i
          recurse 2 (FT a b c d e f g h i) = FT a b (c+1) d e f g h i
          recurse 3 (FT a b c d e f g h i) = FT a b c (d+1) e f g h i
          recurse 4 (FT a b c d e f g h i) = FT a b c d (e+1) f g h i
          recurse 5 (FT a b c d e f g h i) = FT a b c d e (f+1) g h i
          recurse 6 (FT a b c d e f g h i) = FT a b c d e f (g+1) h i
          recurse 7 (FT a b c d e f g h i) = FT a b c d e f g (h+1) i
          recurse _ (FT a b c d e f g h i) = FT a b c d e f g h (i+1)

total :: FishTracker -> Int
total (FT a b c d e f g h i) = a + b + c + d + e + f + h + h + i

splitOn :: (a -> Bool) -> [a] -> [[a]]
splitOn f [] = []
splitOn f as
    | null r    = [l]
    | otherwise = l : splitOn f (tail r)
    where (l,r) = break f as

days1,days2 :: Int
days1 = 80
days2 = 256

repeatCall :: (a->a)->Int->a->a
repeatCall _ 0 x = x
repeatCall f i x = repeatCall f (i-1) $ f x

main :: IO ()
main = do
    initial <- initTracker . map read . splitOn (== ',') <$> readFile "Day6.txt"

    putStrLn $ "Part 1: " ++ show (total $ repeatCall advanceDay days1 initial)
    putStrLn $ "Part 2: " ++ show (total $ repeatCall advanceDay days2 initial)