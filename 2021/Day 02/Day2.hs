data Step = For Int | Up Int | Down Int deriving Show

parseStep :: String -> Step
parseStep a
  | dir == "forward" = For len
  | dir == "up" = Up len
  | otherwise = Down len
  where
      dir : lenStr : _ = words a
      len = read lenStr

{- Moment1 (hoz) (depth) -}
data Moment1 = Moment1 Int Int

{- Moment2 (hoz) (depth) (aim) -}
data Moment2 = Moment2 Int Int Int deriving Show

runStep1 :: Moment1 -> Step -> Moment1
runStep1 (Moment1 hoz depth)  (For d) = Moment1 (hoz + d) depth
runStep1 (Moment1 hoz depth)   (Up d) = Moment1 hoz (depth - d)
runStep1 (Moment1 hoz depth) (Down d) = Moment1 hoz (depth + d)

runStep2 :: Moment2 -> Step -> Moment2
runStep2 (Moment2 hoz depth aim)  (For d) = Moment2 (hoz + d) (depth + aim * d) aim
runStep2 (Moment2 hoz depth aim)   (Up d) = Moment2 hoz depth (aim - d)
runStep2 (Moment2 hoz depth aim) (Down d) = Moment2 hoz depth (aim + d)

runAllSteps1 :: [Step] -> Moment1
runAllSteps1 = foldl runStep1 (Moment1 0 0)

runAllSteps2 :: [Step] -> Moment2
runAllSteps2 = foldl runStep2 (Moment2 0 0 0) 


val1 :: Moment1 -> Int
val1 (Moment1 a b) = a*b

val2 :: Moment2 -> Int
val2 (Moment2 a b _) = a*b

main :: IO ()
main = do
    steps <- map parseStep . lines <$> readFile "Day2.txt"
    putStrLn $ "P1: " ++ show (val1 $ runAllSteps1 steps)
    putStrLn $ "P2: " ++ show (val2 $ runAllSteps2 steps)