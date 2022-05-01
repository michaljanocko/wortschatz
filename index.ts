// @ts-expect-error
import { Elm } from './src/Main.elm'

Elm.Main.init({
  node: document.getElementById('app'),
  flags: localStorage.getItem('notionToken')
})