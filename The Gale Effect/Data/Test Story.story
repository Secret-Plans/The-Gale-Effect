text "Hey this is text"
prompt "Input>", ["test"]
switch
    case "test"
        text: "Hey this is a scope"
    end

    case "other test"
        text: "Hey this is different"
    end
end

text: "Hey this is the end"
exit