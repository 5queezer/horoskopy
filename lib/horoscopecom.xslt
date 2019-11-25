<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:param name="origin"/>
<xsl:variable name="uri">
    https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=%s
</xsl:variable>
<xsl:variable name="zodiacs">
    1 2 3 4 5 6 7 8 9 10 11 12
</xsl:variable>
<xsl:template match="/html">
    <html lang="en">
        <head>
            <meta name="url" content="{$origin}"/>
            <title><xsl:value-of select="head/title"/></title>
        </head>
        <body>
            <p><xsl:value-of select=".//div[@main-horoscope]/p[1]"/></p>
        </body>
    </html>
</xsl:template>
</xsl:stylesheet>