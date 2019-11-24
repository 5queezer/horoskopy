<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/" >
    <html lang="de">
        <head>
            <title><xsl:value-of select="/html/body/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/h2[2]"/></title>
        </head>
        <body>
            <h1><xsl:value-of select="/html/body/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/h2[2]"/></h1>
            <h2><xsl:value-of select="/html/body/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/h2[2]"/></h2>
            <p><xsl:value-of select="p[1]"/></p>
        </body>
    </html>
</xsl:template>
</xsl:stylesheet>