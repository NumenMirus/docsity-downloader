def blurred_parser(blurred):
    imgs = []
    for i in blurred:
        for j in i:
            temp = []
            cl = j.get_attribute("class")

            if cl == "dsy-page__image h0":
                link = (j.get_attribute("style"))
                link.replace('background-image: url("', '')
                link.replace('")', '')
                imgs.append(link)
                break
            else:
                images = j.find_elements_by_tag_name('img')
                for k in images:
                    temp.append(k.get_attribute("src"))
                    for l in temp:
                        if "documents_pages_blur" in l:
                            imgs.append(l)
                            break
                        else:
                            pass
    res = set(imgs)
    return res