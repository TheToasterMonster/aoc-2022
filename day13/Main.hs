module Main where

import Control.Applicative
import Data.Char
import Data.List
import Data.Maybe

newtype Parser a = Parser { run :: String -> Maybe (a, String) }

instance Functor Parser where
  fmap :: (a -> b) -> Parser a -> Parser b
  fmap f (Parser p) = Parser $ \input -> do
    (x, input') <- p input
    return (f x, input')

instance Applicative Parser where
  pure :: a -> Parser a
  pure x = Parser $ \input -> Just (x, input)
  
  (<*>) :: Parser (a -> b) -> Parser a -> Parser b
  (Parser a) <*> (Parser b) = Parser $ \input -> do
    (f, input') <- a input
    (x, input'') <- b input'
    return (f x, input'')

instance Alternative Parser where
  empty :: Parser a
  empty = Parser $ \input -> Nothing
  
  (<|>) :: Parser a -> Parser a -> Parser a
  (Parser a) <|> (Parser b) = Parser $ \input ->
    case a input of
      Just (x, input') -> Just (x, input')
      Nothing -> b input

data ListExpr = Number Integer
              | List [ListExpr]

concatWith :: a -> [[a]] -> [a]
concatWith _ [] = []
concatWith _ [y] = y
concatWith x (y:ys) = y ++ [x] ++ concatWith x ys

instance Show ListExpr where
  show :: ListExpr -> String
  show (Number x) = show x
  show (List xs) = "[" <> (concatWith ',' $ map show xs) <> "]"

instance Eq ListExpr where
  (==) :: ListExpr -> ListExpr -> Bool
  (Number x) == (Number y) = x == y
  (List xs) == (List ys) = xs == ys
  (List xs) == (Number y) = xs == [Number y]
  (Number x) == (List ys) = [Number x] == ys

charP :: (Char -> Bool) -> Parser Char
charP p = Parser $ \input -> case input of
  (x:xs) -> if p x
               then Just (x, xs)
               else Nothing
  _ -> Nothing

whileP :: (Char -> Bool) -> Parser [Char]
whileP p = ((\x xs -> x:xs) <$> charP p <*> whileP p) <|> sequenceA [charP p]

manyP :: Parser a -> Parser [a]
manyP ps = ((\x xs -> x:xs) <$> ps <*> manyP ps) <|> sequenceA [ps]

optP :: Parser a -> Parser [a]
optP ps = (manyP ps) <|> (Parser $ \input -> Just ([], input))

numberP :: Parser ListExpr
numberP = (Number . read) <$> whileP (isDigit)

listP :: Parser ListExpr
listP = List <$> (charP (=='[') *> contents <* charP (==']'))
  where contents = optP ((optP $ charP (==',')) *> exprP <* (optP $ charP (==',')))

exprP :: Parser ListExpr
exprP = numberP <|> listP

instance Ord ListExpr where
  (<=) :: ListExpr -> ListExpr -> Bool
  (Number x) <= (Number y) = x <= y
  (List xs) <= (List ys)
    | xs == [] = True
    | ys == [] = False
    | head xs < head ys = True
    | head xs > head ys = False
    | otherwise = tail xs <= tail ys
  (List xs) <= (Number y) = List xs <= List [Number y]
  (Number x) <= (List ys) = List [Number x] <= List ys

splitOn :: Eq a => a -> [a] -> [[a]]
splitOn x xs = reverse $ map reverse $ filter (/= []) $ splitOnR x xs [[]]
  where
    splitOnR :: Eq a => a -> [a] -> [[a]] -> [[a]]
    splitOnR x (y:ys) acc =
        if x == y
           then splitOnR x ys ([]:acc)
           else splitOnR x ys ((y:head acc):tail acc)
    splitOnR _ [] acc = acc

solvePart1 :: [(Integer, [ListExpr])] -> Integer
solvePart1 = sum
  . map (\(i, [x, y]) ->
         if x < y
            then i
            else 0)

div1 :: ListExpr
div1 = List [List [Number 2]]

div2 :: ListExpr
div2 = List [List [Number 6]]

solvePart2 :: [ListExpr] -> Integer
solvePart2 xs =
  let sorted = sort (div1:div2:xs) in
  let div1Index = fromIntegral $ fromMaybe (-1) $ elemIndex div1 sorted in
  let div2Index = fromIntegral $ fromMaybe (-1) $ elemIndex div2 sorted in
    (div1Index + 1) * (div2Index + 1)

filePath :: FilePath
filePath = "./input.txt"

main :: IO ()
main = do
  file <- readFile filePath
  let input = map (map (fst . fromMaybe (List [], "") . run exprP))
            $ splitOn ""
            $ lines file
  putStr "Part 1: "
  putStrLn $ show $ solvePart1 $ zip [1..] input
  putStr "Part 2: "
  putStrLn $ show $ solvePart2 $ concat input
