module Route exposing (..)

import Url exposing (Url)
import Url.Parser as Parser exposing (Parser, oneOf, s)


type Route
    = NotFound
    | Initial


parser : Parser (Route -> a) a
parser =
    oneOf
        [ Parser.map Initial Parser.top
        ]


fromUrl : Url -> Route
fromUrl url =
    Parser.parse parser url
        |> Maybe.withDefault NotFound
