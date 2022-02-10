def findnewbullets(onebullet,formerbulletlists,threshold):
    for formerbullet in formerbulletlists:
        result = (
            (
            (
            (onebullet[0] - formerbullet[0])**2
            ) + 
            ((onebullet[1] - formerbullet[1])**2) 
            )**0.5)
        if  result<threshold:
            return False
    return True