from PySide2.QtGui import QColor

class PastelColors:
    snow            = QColor(255, 250, 250)
    snow_2          = QColor(238, 233, 233)
    snow_3          = QColor(205, 201, 201)
    ghost_white     = QColor(248, 248, 255)
    white_smoke     = QColor(245, 245, 245)
    gainsboro       = QColor(220, 220, 220)
    floral_white    = QColor(255, 250, 240)
    old_lace        = QColor(253, 245, 230)
    linen           = QColor(240, 240, 230)
    antique_white   = QColor(250, 235, 215)
    antique_white_2 = QColor(238, 223, 204)
    antique_white_3 = QColor(205, 192, 176)
    papaya_whip     = QColor(255, 239, 213)
    blanched_almond = QColor(255, 235, 205)
    bisque          = QColor(255, 228, 196)
    bisque_2        = QColor(238, 213, 183)
    bisque_3        = QColor(205, 183, 158)
    bisque_4        = QColor(139, 125, 107)
    peach_puff      = QColor(255, 218, 185)
    peach_puff_2    = QColor(238, 203, 173)
    peach_puff_3    = QColor(205, 175, 149)
    navajo_white    = QColor(255, 222, 173)
    moccasin        = QColor(255, 228, 181)
    cornsilk        = QColor(255, 248, 220)
    cornsilk_2      = QColor(238, 232, 205)
    cornsilk_3      = QColor(205, 200, 177)
    cornsilk_4      = QColor(139, 136, 120)
    ivory           = QColor(255, 255, 240)
    ivory_2         = QColor(238, 238, 224)
    ivory_3         = QColor(205, 205, 193)
    lemon_chiffon   = QColor(255, 250, 205)
    seashell        = QColor(255, 245, 238)
    seashell_2      = QColor(238, 229, 222)
    seashell_3      = QColor(205, 197, 191)
    honeydew        = QColor(240, 255, 240)
    honeydew_2      = QColor(244, 238, 224)
    honeydew_3      = QColor(193, 205, 193)
    mint_cream      = QColor(245, 255, 250)
    azure           = QColor(240, 255, 255)
    alice_blue      = QColor(240, 248, 255)
    lavender        = QColor(230, 230, 250)
    lavender_blush  = QColor(255, 240, 245)
    misty_rose      = QColor(255, 228, 225)

    full_list = [
        QColor(255, 250, 250), # snow            
        QColor(238, 233, 233), # snow_2          
        QColor(205, 201, 201), # snow_3          
        QColor(248, 248, 255), # ghost_white     
        QColor(245, 245, 245), # white_smoke     
        QColor(220, 220, 220), # gainsboro       
        QColor(255, 250, 240), # floral_white    
        QColor(253, 245, 230), # old_lace        
        QColor(240, 240, 230), # linen           
        QColor(250, 235, 215), # antique_white   
        QColor(238, 223, 204), # antique_white_2 
        QColor(205, 192, 176), # antique_white_3 
        QColor(255, 239, 213), # papaya_whip     
        QColor(255, 235, 205), # blanched_almond 
        QColor(255, 228, 196), # bisque          
        QColor(238, 213, 183), # bisque_2        
        QColor(205, 183, 158), # bisque_3        
        QColor(139, 125, 107), # bisque_4        
        QColor(255, 218, 185), # peach_puff      
        QColor(238, 203, 173), # peach_puff_2    
        QColor(205, 175, 149), # peach_puff_3    
        QColor(255, 222, 173), # navajo_white    
        QColor(255, 228, 181), # moccasin        
        QColor(255, 248, 220), # cornsilk        
        QColor(238, 232, 205), # cornsilk_2      
        QColor(205, 200, 177), # cornsilk_3      
        QColor(255, 255, 240), # ivory           
        QColor(238, 238, 224), # ivory_2         
        QColor(205, 205, 193), # ivory_3         
        QColor(255, 250, 205), # lemon_chiffon   
        QColor(255, 245, 238), # seashell        
        QColor(238, 229, 222), # seashell_2      
        QColor(205, 197, 191), # seashell_3      
        QColor(240, 255, 240), # honeydew        
        QColor(244, 238, 224), # honeydew_2      
        QColor(193, 205, 193), # honeydew_3      
        QColor(245, 255, 250), # mint_cream      
        QColor(240, 255, 255), # azure           
        QColor(240, 248, 255), # alice_blue      
        QColor(230, 230, 250), # lavender        
        QColor(255, 240, 245), # lavender_blush  
        QColor(255, 228, 225), # misty_rose      
    ]

    @staticmethod
    def color_for_string(s):
        h = s.__hash__()
        l = len(PastelColors.full_list)
        return PastelColors.full_list[h % l]

