<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:junos="http://xml.juniper.net/junos/*/junos" xmlns:xnm="http://xml.juniper.net/xnm/1.1/xnm" xmlns:jcs="http://xml.juniper.net/junos/commit-scripts/1.0" xmlns:ext="http://xmlsoft.org/XSLT/namespace" version="1.0">
  <xsl:import href="../import/junos.xsl"/>
  <!-- 
 * This commit-script ensures that BGP both exists and is active.
 * This could be obviously used for any other protocol.
 * This example is taken from:
 * https://github.com/Juniper/junoscriptorium/blob/master/library/juniper/commit/protocols/bgp-active/
 * Generated from the SLAX version with: 
 * request system scripts convert slax-to-xslt source $file destination $file
 -->
  <xsl:template match="configuration">
    <xsl:for-each select="protocols/bgp/node()">
      <xsl:variable name="line" select="name()"/>
      <xsl:if test="$line = &quot;disable&quot;">
        <xnm:warning>
          <message>BGP has been disabled</message>
        </xnm:warning>
      </xsl:if>
    </xsl:for-each>
    <xsl:variable name="bgp" select="protocols/bgp"/>
    <xsl:if test="not($bgp)">
      <xnm:error>
        <message>BGP deactivated or deleted.</message>
      </xnm:error>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
