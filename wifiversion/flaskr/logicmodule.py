# it marks if bullet is newone. get formerbullets, and compare, 
# then if the bullet is very close(smaller than threshold), consider it as already checked.
def findnewbullets(onebullet,formerbulletdicts,threshold):
    for formerbullet in formerbulletdicts:
        result = (
            (
            (
            (onebullet[0] - formerbullet["xposition"])**2
            ) + 
            ((onebullet[1] - formerbullet["yposition"])**2) 
            )**0.5)
        if  result<threshold:
            return False
    return True