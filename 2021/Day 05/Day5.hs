import Data.Map.Strict
    ( Map, insert, empty, toList, findWithDefault )

type Point = (Int,Int)
type Line = (Point, Point)
type Grid = Map Point Int

isHozOrVert :: Line -> Bool
isHozOrVert ((a,b),(c,d)) = a == c || b == d

addPoint :: Point -> Point -> Point
addPoint (a,b) (c,d) = (a+c, b+d)

{- recursively draws a line on a grid -}
{- first point is where you are at, second is where you are going until, third is step direction -}
drawLine' :: Grid -> Point -> Point -> Point -> Grid
drawLine' g x y d
    | x == y    = insert x (1 + findWithDefault 0 x g) g
    | otherwise = insert x (1 + findWithDefault 0 x g) $ drawLine' g (addPoint x d) y d
    
unitDir :: Point -> Point -> Point
unitDir (a,b) (c,d) = (dir a c, dir b d)
    where dir x y = (y-x) `div` max (abs (y-x)) 1

drawLine :: Line -> Grid -> Grid
drawLine (x, y) g = drawLine' g x y $ unitDir x y

drawAllLines :: Grid -> [Line] -> Grid
drawAllLines = foldr drawLine


splitOn :: (a -> Bool) -> [a] -> [[a]]
splitOn f [] = []
splitOn f as
    | null r    = [l]
    | otherwise = l : splitOn f (tail r)
    where (l,r) = break f as

{- this one would be annoying without using the parse functor -}
parseLine :: String -> Line
parseLine l = ((read a,read b),(read c,read d))
    where (start:(_:fin):_) = splitOn (== '-') l
          (a:b:_) = splitOn (== ',') start
          (c:d:_) = splitOn (== ',') fin

countMultiple :: Grid -> Int
countMultiple = length . filter (\(_,b)->b>=2) . toList

main :: IO ()
main = do
    lines <- map parseLine . lines <$> readFile "Day5.txt"
    putStrLn $ "Part 1: " ++ show (countMultiple $ drawAllLines empty $ filter isHozOrVert lines)
    putStrLn $ "Part 2: " ++ show (countMultiple $ drawAllLines empty lines)