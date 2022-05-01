module Main exposing (main)

import Browser
import Browser.Navigation as Nav
import Html exposing (..)
import Html.Attributes as Attr
import Url exposing (Url)
import Url.Builder exposing (string)


main : Program (Maybe String) Model Msg
main =
    Browser.application
        { init = init
        , update = update
        , subscriptions = always Sub.none
        , view =
            \model ->
                { title = "Wortschatz"
                , body = view model
                }
        , onUrlRequest = ClickedLink
        , onUrlChange = UrlChanged
        }



-- INIT


init : Maybe String -> Url -> Nav.Key -> ( Model, Cmd Msg )
init prevSession url key =
    ( case prevSession of
        Just token ->
            { key = key }

        Nothing ->
            { key = key }
    , Cmd.none
    )


type alias Model =
    { key : Nav.Key }



-- UPDATE


type Msg
    = ClickedLink Browser.UrlRequest
    | UrlChanged Url


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ClickedLink urlRequest ->
            case urlRequest of
                Browser.Internal url ->
                    ( model, Nav.pushUrl model.key (Url.toString url) )

                Browser.External href ->
                    ( model, Nav.load href )

        UrlChanged url ->
            ( model, Cmd.none )



-- VIEW


view : Model -> List (Html Msg)
view model =
    [ main_ [ Attr.class "container" ]
        [ a [ Attr.href loginUrl ]
            [ text "Mit Notion anmelden" ]
        ]
    ]


loginUrl : String
loginUrl =
    Url.Builder.crossOrigin "https://api.notion.com"
        [ "v1", "oauth", "authorize" ]
        [ string "client_id" "fce9c87e-3860-47c6-b9a6-65ffc789a2b8"
        , string "redirect_uri" "http://localhost:1234/callback"
        , string "response_type" "code"
        , string "owner" "user"
        , string "state" "ahojda"
        ]
