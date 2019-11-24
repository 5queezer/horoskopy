<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:param name="uri" />
<xsl:template match="/html" >
    <html lang="de">
        <head>
            <meta name="url" content="{$uri}"/>
            <title><xsl:value-of select="head/title"/></title>
        </head>
        <body>
            <dl>
                <xsl:for-each select="body//div[@class='horoscope-item-right']/h3">
                    <dt><xsl:value-of select="text()"/></dt>
                    <dd><xsl:value-of select="following-sibling::p[1]/text()"/></dd>
                </xsl:for-each>
            </dl>
        </body>
    </html>
</xsl:template>
</xsl:stylesheet>
