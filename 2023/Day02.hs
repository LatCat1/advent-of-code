import Text.ParserCombinators.ReadP
    ( ReadP, char, munch1, readP_to_S, sepBy, skipSpaces, string )
import Data.Char (isDigit)
import Control.Applicative ((<|>))
import Data.Functor (($>))

data Color = Red | Green | Blue deriving (Eq, Show)

data Draw = Draw {
    color :: Color,
    count :: Int
} deriving (Show, Eq)


readColor :: ReadP Color
readColor = 
    foldr1 (<|>) $ zipWith (\c1 c2 -> string c1 $> c2) ["red", "green", "blue"] [Red, Green, Blue]

readOneDraw :: ReadP Draw
readOneDraw = do
    skipSpaces
    n <- munch1 isDigit
    skipSpaces
    color <- readColor
    return $ Draw {color=color, count=read n}

instance Read Draw where
    readsPrec :: Int -> ReadS Draw
    readsPrec _ = readP_to_S readOneDraw

data Bag = Bag { id_num :: Int, red :: Int, green :: Int, blue :: Int } deriving (Show, Eq)

emptyBag :: Int -> Bag
emptyBag x = Bag {id_num=x, red=0, green=0, blue=0}

updateBag :: Draw -> Bag -> Bag
updateBag (Draw Red n) b = b {red = max n (red b)}
updateBag (Draw Blue n) b = b {blue = max n (blue b)}
updateBag (Draw Green n) b = b {green = max n (green b)}

readBag :: ReadP Bag
readBag = do
    string "Game "
    n <- read <$> munch1 isDigit
    char ':'
    draws <- sepBy readOneDraw (char ',' <|> char ';')
    return $ foldr updateBag (emptyBag n) draws

instance Read Bag where
    readsPrec :: Int -> ReadS Bag
    readsPrec _ = readP_to_S readBag

legalBag :: Int -> Int -> Int -> Bag -> Bool
legalBag r g b (Bag _ r' g' b') = and $ zipWith (<=) [r', g', b'] [r, g, b]

powerset :: Bag -> Int
powerset (Bag _ r g b) = r * g * b

main :: IO ()
main = do
    text <- getContents
    let realLines = filter ((/=) 0 . length) $ lines text
    let bags :: [Bag] = map read realLines
    let p1 = sum $ id_num <$> filter (legalBag 12 13 14) bags
    let p2 = sum $ powerset <$> bags
    putStrLn $ "Part 1: " ++ show p1 ++ "\nPart 2: " ++ show p2 ++ "\n"