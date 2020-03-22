set d "Input>"

text "12:35 - Spanish"
text "You kinda need to go to the bathroom."
prompt $d ["bathroom", "die"]
switch
    case "bathroom"
        text "You ask if you can go to the bathroom."
        text "The teacher is suspicious but allows it."
        text "It's a recent policy."
        prompt $d ["test"]
        switch
            case "test"
                text "That worked"
            end
         end
    end

    case "die"
        text "You die"
        exit
    end
end

text "Hey this is the end"
exit
