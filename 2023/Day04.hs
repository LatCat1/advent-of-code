import Text.ParserCombinators.ReadP
    ( ReadP, char, munch1, readP_to_S, sepBy, skipSpaces, string , (+++))
import Data.Char (isDigit)
import Data.Functor (($>))
import GHC.Utils.Misc (count)
import Data.Map.Strict (Map, (!), findWithDefault, adjust, fromList)

data Card = Card {id_num::Int, mine::[Int], wins::[Int]} deriving (Show)

readCard :: ReadP Card
readCard = do
    string "Card"
    skipSpaces
    id_num <- read <$> munch1 isDigit
    string ":"
    skipSpaces
    winNums <- map read <$> sepBy (munch1 isDigit) skipSpaces
    skipSpaces
    char '|'
    skipSpaces
    myNums <- map read <$> sepBy (munch1 isDigit) skipSpaces
    skipSpaces
    return $ Card {id_num=id_num, wins=winNums, mine=myNums}

instance Read Card where
    readsPrec :: Int -> ReadS Card
    readsPrec _ = readP_to_S readCard

matches :: Card -> Int
matches c = count (`elem` wins c) $ mine c

points :: Int -> Int
points 0 = 0
points n = 2 ^ (n-1)

part1 :: String -> Int
part1 = sum . map (points . matches . read) . lines

score :: Map Int Int -> Card ->  Map Int Int
score copies c = foldr (adjust (+c_count)) copies [(id_num c+1)..(id_num c + c_matches)]
    where c_count = findWithDefault 0 (id_num c) copies
          c_matches = matches c

part2 :: String -> Int
part2 s = sum $ foldl score (fromList $ map (,1) [1..length ls]) ls
    where ls :: [Card] = read <$> lines s

main :: IO ()
main = do
    text <- getContents
    putStrLn "Part 1: " 
    print $ part1 text
    putStrLn "Part 2: "