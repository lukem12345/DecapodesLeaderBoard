# DecapodesLeaderBoard

DecapodesLeaderBoard is a site for documenting example physics simulations.

See the [Decapodes.jl repo](https://github.com/AlgebraicJulia/Decapodes.jl) for more on the framework itself.

## Architecture Choices

Since this site is designed to be feature-light (basic toggling, storing state in the query string), I decided to set it up as a CGI app. Racket is a good choice due to its `scribble/html` library, which lets you write html directly in the source in a single-file architecture without sacrificing readability:

```racket
;; A form for toggling state of the webpage.
(define view-configuration
  (form action:"./dlb.cgi" method:"GET"
        (hiding-checkbox "leaderboard") (hiding-checkbox "plots") (hiding-checkbox "diagrams")
        (input type:"submit" value:"Show")))
```

Functions that return HTML programmatically (widgets) are easy to write:

```racket
;; A widget for checkboxes that hide elements according to a global variable.
(define (hiding-checkbox to-show)
  (define id (~a "show-" to-show))
  (define label-val (string-titlecase to-show))
  (define checked (checked-attr (eval (string->symbol id) ns)))
  (div class:"hiding-checkbox"
       (label for: id label-val)
       (apply element 'input 'type: "checkbox" 'id: id 'name: id 'value: "T" checked)))
```

Organizing content can be accomplished without any heavy frameworks:

```racket
;; The layout of the webpage.
(define (front-page)
  (body
   floating-header
   (div class:"main-content"
        instructions
        leader-board
        scenario-showcase
        decapodes-overview)
   footer))
```

