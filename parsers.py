def blurred_parser(blurred):
    imgs = []
    for i in blurred:
        for j in i:
            cl = j.get_attribute("class")

            if cl == "dsy-page__image h0":
                imgs.append(j.get_attribute("style"))
                print("added")
                break
            else:
                images = j.find_elements_by_tag_name('img')
                for k in images:
                    temp = k.get_attribute("src")
                    for l in temp:
                        if "documents" in l:
                            print(l)
                        else:
                            print("non c'è nulla")
    
            
    
    for i in imgs:
        print(i)