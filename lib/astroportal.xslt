<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:param name="origin"/>
<xsl:variable name="uri">
    https://www.astroportal.com/tageshoroskope/%s/
</xsl:variable>
<xsl:variable name="zodiacs">
    widder stier zwillinge krebs loewe jungfrau waage skorpion schuetze steinbock wassermann fische
</xsl:variable>
<xsl:template match="/html">
    <html lang="de">
        <head>
            <meta name="url" content="{$origin}"/>
            <title><xsl:value-of select="head/title"/></title>
        </head>
        <body>
            <h1><xsl:value-of select="body//h3[@class='blue']"/></h1>
            <p><xsl:value-of select="body//h3[@class='blue']/following-sibling::p"/></p>
        </body>
    </html>
</xsl:template>
</xsl:stylesheet>